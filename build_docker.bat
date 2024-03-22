docker build -t dactyl-keyboard -f docker/Dockerfile .
docker run --name DM-run -d -v "S:/temp/dactyl/src:/app/src" -v "S:/temp/dactyl/things:/app/things" -v "S:/temp/dactyl/things:/app/configs"  dactyl-keyboard python3 -i dactyl_manuform.py
docker run --name DM-config -d -v "S:/temp/dactyl/src:/app/src" -v "S:/temp/dactyl/things:/app/things" -v "S:/temp/dactyl/things:/app/configs" dactyl-keyboard python3 -i generate_configuration.py
docker run --name DM-release-build -d -v "S:/temp/dactyl/src:/app/src" -v "S:/temp/dactyl/things:/app/things" -v "S:/temp/dactyl/things:/app/configs" dactyl-keyboard python3 -i model_builder.py
docker run --name DM-shell -d -ti -v "S:/temp/dactyl/src:/app/src" -v "S:/temp/dactyl/things:/app/things"  -v "S:/temp/dactyl/things:/app/configs" dactyl-keyboard
