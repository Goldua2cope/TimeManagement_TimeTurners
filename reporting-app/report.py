import argparse
from report_builder import build_report_text, save_report_to_file

def main():
    parser = argparse.ArgumentParser(description="Generate consultant time report")
    parser.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="End date YYYY-MM-DD")
    parser.add_argument("--upload", action="store_true", help="Also upload to Blob Storage")
    args = parser.parse_args()

    text = build_report_text(args.start, args.end)
    print(text)
    filename = save_report_to_file(text, f"report_{args.start}_to_{args.end}.txt")

    if args.upload:
        from upload import upload_report
        upload_report(filename, filename)

if __name__ == "__main__":
    main()