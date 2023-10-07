Dockerfile.graphite_realy
  Switch graphite relay back to python base
  Do i need to expose port 1433?

Dockerfile.rtl433
  switch to a build container and move the needed bits to final image
  add `"-C", "customary"` flag to convert to US units?

Docker-compose.yml
  DO i need to call out port 1433 since its just for the two containers to communicate?
