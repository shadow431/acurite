#docker compose --file docker-compose-grayland.yml --env-file prod.env up -d
docker run -it --rm --device=/dev/bus/usb:/dev/bus/usb allgeek_rtlsdr:bec
