
def get_status_code_range(row: str) -> tuple[int | None, int | None]:
    if not row: return (None, None)
    row = row.replace(' ', '').strip()
    start, _, end = row.partition('-')
    start = int(start)
    if end: end = int(end)
    else: end = start
    return start, end