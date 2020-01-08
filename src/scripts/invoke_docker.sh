#/usr/bin/env sh
echo "Launching Docker Image with env"
echo -e "OTX_API_KEY="$1
echo -e "RULES_FILE="$2
echo -e "REFRESH_RATE="$3

docker run -e OTX_API_KEY=$1 -e RULES_FILE=$2 -e REFRESH_RATE=$3 zerotrust-feed:1.0.dev0 python -m ZeroTrustUpdateBackEnd

