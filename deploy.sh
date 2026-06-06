gcloud functions deploy guitar_to_dulcimer_tab \
  --project=dulcimer-tab \
  --region=europe-west1 \
  --runtime=python312 \
  --source=. \
  --set-build-env-vars=GOOGLE_FUNCTION_SOURCE=tab_converter.py \
  --entry-point=guitar_to_dulcimer_tab \
  --trigger-http \
  --allow-unauthenticated

gcloud functions deploy midi_to_dulcimer_tab \
  --project=dulcimer-tab \
  --region=europe-west2 \
  --runtime=python312 \
  --source=. \
  --set-build-env-vars=GOOGLE_FUNCTION_SOURCE=tab_converter.py \
  --entry-point=midi_to_dulcimer_tab \
  --trigger-http \
  --allow-unauthenticated


firebase deploy
