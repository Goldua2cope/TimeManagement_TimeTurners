from datetime import date
from queries import get_hours_per_consultant, get_hours_per_customer, get_average_hours_per_consultant

def build_report_text(start_date, end_date):
    consultant_data = get_hours_per_consultant(start_date, end_date)
    customer_data = get_hours_per_customer(start_date, end_date)
    avg_data = get_average_hours_per_consultant(start_date, end_date)

    lines = []
    lines.append(f"Time Report: {start_date} to {end_date}")
    lines.append("=" * 40)
    lines.append("")

    lines.append("Hours per consultant:")
    for name, hours in consultant_data:
        lines.append(f"  {name}: {hours}h")
    lines.append("")

    lines.append("Cumulative hours per customer (all consultants):")
    for name, hours in customer_data:
        lines.append(f"  {name}: {hours}h")
    lines.append("")

    lines.append("Average hours per day per consultant:")
    for name, avg_hours in avg_data:
        lines.append(f"  {name}: {avg_hours}h/day")

    return "\n".join(lines)

def save_report_to_file(text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Report saved to {filename}")
    return filename

if __name__ == "__main__":
    text = build_report_text("2026-08-01", "2026-08-31")
    print(text)
    save_report_to_file(text, "report_2026-08-01_to_2026-08-31.txt")