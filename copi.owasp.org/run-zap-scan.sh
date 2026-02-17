#!/bin/bash

# OWASP ZAP DAST Scan Script for Copi Application
# This script runs a ZAP security scan against the locally running Copi application

set -e

# Configuration
TARGET_URL="${TARGET_URL:-http://localhost:4000/games/new}"
REPORT_DIR="${REPORT_DIR:-./zap-reports}"
ZAP_IMAGE="ghcr.io/zaproxy/zaproxy:stable"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== OWASP ZAP DAST Scanner for Copi ===${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Check if application is running
echo -e "${YELLOW}Checking if Copi application is running...${NC}"
if ! curl -f -s "$TARGET_URL" > /dev/null 2>&1; then
    echo -e "${RED}Error: Copi application is not accessible at $TARGET_URL${NC}"
    echo "Please start the application first:"
    echo "  cd copi.owasp.org"
    echo "  mix phx.server"
    exit 1
fi
echo -e "${GREEN}✓ Application is running${NC}"
echo ""

# Create report directory
mkdir -p "$REPORT_DIR"
echo -e "${YELLOW}Reports will be saved to: $REPORT_DIR${NC}"
echo ""

# Pull latest ZAP image
echo -e "${YELLOW}Pulling latest ZAP Docker image...${NC}"
docker pull "$ZAP_IMAGE"
echo ""

# Run ZAP scan
echo -e "${GREEN}Starting ZAP Full Scan...${NC}"
echo -e "${YELLOW}Target: $TARGET_URL${NC}"
echo -e "${YELLOW}This may take 30-45 minutes...${NC}"
echo ""

docker run --rm --network="host" \
    -v "$(pwd)/$REPORT_DIR:/zap/wrk/:rw" \
    -t "$ZAP_IMAGE" \
    zap-full-scan.py \
    -t "$TARGET_URL" \
    -r copi_dast_report.html \
    -w copi_dast_report.md \
    -J copi_dast_report.json \
    -x copi_dast_report.xml \
    -a \
    -j \
    -d \
    -m 10 \
    -T 30 \
    || true

echo ""
echo -e "${GREEN}=== Scan Complete ===${NC}"
echo ""

# Check for reports
if [ -f "$REPORT_DIR/copi_dast_report.json" ]; then
    echo -e "${GREEN}✓ Reports generated successfully${NC}"
    echo ""
    echo "Available reports:"
    ls -lh "$REPORT_DIR"
    echo ""
    
    # Parse and display vulnerability summary
    if command -v jq > /dev/null 2>&1; then
        echo -e "${YELLOW}=== Vulnerability Summary ===${NC}"
        
        HIGH=$(jq '[.site[].alerts[] | select(.riskcode == "3")] | length' "$REPORT_DIR/copi_dast_report.json" 2>/dev/null || echo "0")
        MEDIUM=$(jq '[.site[].alerts[] | select(.riskcode == "2")] | length' "$REPORT_DIR/copi_dast_report.json" 2>/dev/null || echo "0")
        LOW=$(jq '[.site[].alerts[] | select(.riskcode == "1")] | length' "$REPORT_DIR/copi_dast_report.json" 2>/dev/null || echo "0")
        INFO=$(jq '[.site[].alerts[] | select(.riskcode == "0")] | length' "$REPORT_DIR/copi_dast_report.json" 2>/dev/null || echo "0")
        
        echo -e "High Risk:   ${RED}$HIGH${NC}"
        echo -e "Medium Risk: ${YELLOW}$MEDIUM${NC}"
        echo -e "Low Risk:    $LOW"
        echo -e "Info:        $INFO"
        echo ""
        
        if [ "$HIGH" -gt "0" ]; then
            echo -e "${RED}⚠️  WARNING: High-risk vulnerabilities detected!${NC}"
            echo -e "${RED}   Please review the report immediately.${NC}"
            echo ""
        fi
    else
        echo -e "${YELLOW}Install 'jq' to see vulnerability summary${NC}"
        echo ""
    fi
    
    echo "To view the HTML report:"
    echo -e "  ${GREEN}open $REPORT_DIR/copi_dast_report.html${NC}"
    echo ""
    echo "Or on Linux:"
    echo -e "  ${GREEN}xdg-open $REPORT_DIR/copi_dast_report.html${NC}"
    
else
    echo -e "${RED}✗ Reports not found. Check the scan output for errors.${NC}"
    exit 1
fi
