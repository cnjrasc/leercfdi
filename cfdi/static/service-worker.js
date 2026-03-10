const CACHE_NAME = 'cfdipyme-v1';

const urlsToCache = [
    '/',
    '/static/css/bootstrap.min.css',
    '/static/js/bootstrap.bundle.min.js',
];

self.addEventListener("install", function(event) {
    event.waitUntil(
      caches.open("erp-cache").then(function(cache) {
        return cache.addAll([
          "/",
          "/static/manifest.json"
        ]);
      })
    );
  });
  
  self.addEventListener("fetch", function(event) {
    event.respondWith(
      caches.match(event.request).then(function(response) {
        return response || fetch(event.request);
      })
    );
  });