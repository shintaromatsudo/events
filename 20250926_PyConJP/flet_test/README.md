```
uv init
uv add 'flet[all]' --dev
uv run flet create
uv run flet run --web
uv run flet build web
python -m http.server --directory build/web 8888
```
