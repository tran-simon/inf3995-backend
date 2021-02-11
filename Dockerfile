FROM python:3

RUN apt-get update && apt-get install -y \
	usbutils


WORKDIR /root/backend

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_APP=src/app.py
ENV FLASK_ENV=development
ENV PORT=5000

EXPOSE 5000

RUN mkdir  -p /etc/udev/rules.d
RUN echo '# Crazyradio (normal operation) \
          SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="7777", MODE="0664", GROUP="plugdev" \
          # Bootloader \
          SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="0101", MODE="0664", GROUP="plugdev" \
          SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="5740", MODE="0664", GROUP="plugdev" ' > /etc/udev/rules.d/99-crazyradio.rules


CMD ["flask", "run"]
