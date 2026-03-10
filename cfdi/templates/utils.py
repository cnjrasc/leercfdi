from datetime import date
from lxml import etree
import pandas as pd
from io import BytesIO

def convertir_fecha_iso(fecha):
    if isinstance(fecha, str):
        return date.fromisoformat(fecha)
    return None

def extract_cfdi_from_xml(xml_content):
    ns = {
        'cfdi': 'http://www.sat.gob.mx/cfd/4',
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'
    }

    try:
        tree = etree.parse(BytesIO(xml_content))
        root = tree.getroot()

        # Inicializamos montos por tipo
        iva_trasladado = 0
        ieps_trasladado = 0
        iva_retenido = 0
        isr_retenido = 0

        # Traslados
        impuestos = root.find('cfdi:Impuestos', ns)
        if impuestos is not None:
            traslados = impuestos.findall('cfdi:Traslados/cfdi:Traslado', ns)
        else:
            traslados = []

        for t in traslados:
            impuesto = t.get('Impuesto')
            importe = float(t.get('Importe', '0'))
            if impuesto == '002':
                iva_trasladado += importe
            elif impuesto == '003':
                ieps_trasladado += importe

        # Retenciones
        retenciones = []
        impuestos = root.find('cfdi:Impuestos', ns)
        if impuestos is not None:
            retenciones = impuestos.findall('cfdi:Retenciones/cfdi:Retencion', ns)

        for r in retenciones:
            impuesto = r.get('Impuesto')
            importe = float(r.get('Importe', '0'))
            if impuesto == '001':
                isr_retenido += importe
            elif impuesto == '002':
                iva_retenido += importe

        emisor = root.find('cfdi:Emisor', ns)
        receptor = root.find('cfdi:Receptor', ns)
        timbre = root.find('.//tfd:TimbreFiscalDigital', ns)
        conceptos = root.findall('cfdi:Conceptos/cfdi:Concepto', ns)

        subtotal = root.get('SubTotal')
        total = root.get('Total')

        concepto_descripciones = []
        for c in conceptos:
            desc = f"{c.get('Descripcion')} ({c.get('Cantidad')} x {c.get('ValorUnitario')})"
            concepto_descripciones.append(desc)

        conceptos_str = "; ".join(concepto_descripciones)

        uso_cfdi = receptor.get('UsoCFDI') if receptor is not None else ''
        tipo_comprobante = root.get('TipoDeComprobante')
        metodo_pago = root.get('MetodoPago')
        forma_pago = root.get('FormaPago')

        USO_CFDI_DESCRIPCIONES = {
        'G01': 'Adquisición de mercancías',
        'G02': 'Devoluciones, descuentos o bonificaciones',
        'G03': 'Gastos en general',
        'I01': 'Construcciones',
        'P01': 'Por definir'
        # Puedes agregar más según tu catálogo SAT
        }

        TIPO_COMPROBANTE_DESCRIPCIONES = {
        'I': 'Ingreso',
        'E': 'Egreso',
        'T': 'Traslado',
        'N': 'Nómina',
        'P': 'Pago'
        }

        METODO_PAGO_DESCRIPCIONES = {
        'PUE': 'Pago en una sola exhibición',
        'PPD': 'Pago en parcialidades o diferido'
        }

        FORMA_PAGO_DESCRIPCIONES = {
        '01': 'Efectivo',
        '02': 'Cheque nominativo',
        '03': 'Transferencia electrónica',
        '04': 'Tarjeta de crédito',
        '17': 'Compensación',
        '27': 'A satisfacción del acreedor',
        '28': 'Tarjeta de débito'
        # Completa los que necesites
        }

        rows = [{
            'UUID': timbre.get('UUID') if timbre is not None else '',
            'Fecha': root.get('Fecha'),
            'Serie': root.get('Serie'),
            'Folio': root.get('Folio'),
            'RFC_Emisor': emisor.get('Rfc') if emisor is not None else '',
            'Nombre_Emisor': emisor.get('Nombre') if emisor is not None else '',
            'RFC_Receptor': receptor.get('Rfc') if receptor is not None else '',
            'Nombre_Receptor': receptor.get('Nombre') if receptor is not None else '',
            'SubTotal': float(subtotal or 0),
            'Descuento': float(root.get('Descuento', '0')) if root.get('Descuento') else 0,
            'Total': float(total or 0),
            'IVA_Trasladado': iva_trasladado,
            'IEPS_Trasladado': ieps_trasladado,
            'IVA_Retenido': iva_retenido,
            'ISR_Retenido': isr_retenido,
            'Conceptos': conceptos_str,
            'Metodo_Pago': METODO_PAGO_DESCRIPCIONES.get(metodo_pago, metodo_pago),
            'Forma_Pago': FORMA_PAGO_DESCRIPCIONES.get(forma_pago, forma_pago),
            'Tipo_Comprobante': TIPO_COMPROBANTE_DESCRIPCIONES.get(tipo_comprobante, tipo_comprobante),
            'Uso_CFDI': USO_CFDI_DESCRIPCIONES.get(uso_cfdi, uso_cfdi),
        }]
        return rows

    except Exception as e:
        print(f"⚠️ Error procesando CFDI: {e}")
        return []

def cfdi_to_excel(cfdi_data):
    df = pd.DataFrame([cfdi_data])
    return df