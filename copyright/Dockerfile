FROM python:3.12-slim

# Install prerequisites (libicu required by .NET for globalization/CJK support)
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget zip unzip libicu76 && \
    rm -rf /var/lib/apt/lists/*

# Install .NET SDK 8.0 via Microsoft install script
RUN wget -q https://dot.net/v1/dotnet-install.sh -O /tmp/dotnet-install.sh && \
    chmod +x /tmp/dotnet-install.sh && \
    /tmp/dotnet-install.sh --channel 8.0 && \
    rm /tmp/dotnet-install.sh

ENV PATH="/root/.dotnet:${PATH}"
ENV DOTNET_CLI_UI_LANGUAGE=en
ENV DOTNET_NUGET_SIGNATURE_VERIFICATION=false

# Install Python dependencies
RUN pip install --no-cache-dir python-docx

WORKDIR /workspace
