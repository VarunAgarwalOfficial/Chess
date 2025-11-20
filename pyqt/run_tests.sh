#!/bin/bash
# Test runner script for PyQt6 Chess Application

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}PyQt6 Chess - Test Runner${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}pytest is not installed!${NC}"
    echo "Install with: pip install -r requirements-dev.txt"
    exit 1
fi

# Parse arguments
VERBOSE=""
MARKERS=""
COVERAGE=""
SPECIFIC_TEST=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE="-v"
            shift
            ;;
        -m|--markers)
            MARKERS="$2"
            shift 2
            ;;
        -c|--coverage)
            COVERAGE="--cov=src"
            shift
            ;;
        -t|--test)
            SPECIFIC_TEST="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: ./run_tests.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -v, --verbose           Verbose output"
            echo "  -m, --markers MARKERS   Run tests with specific markers"
            echo "  -c, --coverage          Generate coverage report"
            echo "  -t, --test TEST         Run specific test file or class"
            echo "  -h, --help              Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./run_tests.sh                              # Run all tests"
            echo "  ./run_tests.sh -v                           # Verbose output"
            echo "  ./run_tests.sh -m integration               # Only integration tests"
            echo "  ./run_tests.sh -m 'not slow'                # Skip slow tests"
            echo "  ./run_tests.sh -t tests/test_integration.py::TestMainWindow"
            echo "  ./run_tests.sh -c                           # With coverage report"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Build pytest command
CMD="pytest tests/test_integration.py"

if [ -n "$VERBOSE" ]; then
    CMD="$CMD $VERBOSE"
fi

if [ -n "$MARKERS" ]; then
    CMD="$CMD -m '$MARKERS'"
fi

if [ -n "$COVERAGE" ]; then
    CMD="$CMD $COVERAGE"
fi

if [ -n "$SPECIFIC_TEST" ]; then
    CMD="$CMD $SPECIFIC_TEST"
fi

# Run tests
echo -e "${YELLOW}Running:${NC} $CMD"
echo ""

if eval $CMD; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}All tests passed!${NC}"
    echo -e "${GREEN}========================================${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}Tests failed!${NC}"
    echo -e "${RED}========================================${NC}"
    exit 1
fi
