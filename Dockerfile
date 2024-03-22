FROM mambaorg/micromamba
#:0.8.2

USER root

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx gcc bash python3 python3-pip  && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
#RUN micromamba install -y -n base -c conda-forge -c cadquery \
#    python=3 \
#    cadquery=master \
#    numpy=1 \
#    scipy=1 && \
#    (rm /opt/conda/pkgs/cache/* || true)

RUN pip3 install solidpython2 numpy scipy cadquery --break-system-packages
COPY ./ /app/

#WORKDIR /app/src