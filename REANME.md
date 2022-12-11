

```bash
python -m venv pyenv-qs
source pyenv-qs/bin/activate

python -m pip install --user --upgrade google-cloud-pubsub

export GOOGLE_APPLICATION_CREDENTIALS=path_to_file
export PROJECT=`gcloud config get-value project`
```

