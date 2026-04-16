let db;

// Abrir base local
const request = indexedDB.open("erp_cfdi", 1);

request.onupgradeneeded = function(event) {
  db = event.target.result;
  db.createObjectStore("facturas", { keyPath: "uuid" });
};

request.onsuccess = function(event) {
  db = event.target.result;
  console.log("Base local lista");
};

// FUNCION PARA GUARDAR CFDI LOCALMENTE
function guardarFactura(cfdi){

  const tx = db.transaction("facturas", "readwrite");
  const store = tx.objectStore("facturas");

  store.put(cfdi);

  console.log("Factura guardada localmente");

}