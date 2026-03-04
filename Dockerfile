FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt && pip install "fastapi[standard]"

RUN --mount=type=secret,id=grandlyon_pass,env=GRANDLYON_PASS --mount=type=secret,id=grandlyon_user,env=GRANDLYON_USER \
    mkdir -p static && \
    curl -u "$GRANDLYON_USER:$GRANDLYON_PASS" https://download.data.grandlyon.com/files/rdata/tcl_sytral.tclpictogrammes/Pictogrammes_lignes_complets.zip -o picto.zip && \
    unzip picto.zip -d static && \
    rm picto.zip

COPY src .
EXPOSE 8000

ENTRYPOINT ["fastapi", "run", "main.py"]