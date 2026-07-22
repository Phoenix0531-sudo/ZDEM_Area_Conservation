FROM hermes-patent-figs
COPY . /app
WORKDIR /app
CMD python Area_Conservation.py --dir data --colors all --threshold 3.0
