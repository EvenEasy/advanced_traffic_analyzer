from dataclasses import dataclass


@dataclass
class FilterOpt:
    top: int
    start: int
    end: int
    method: str
    start_status: int
    end_status: int

    @property
    def status(self):
        """Human-readable status filter string.

        Returns a string representing the configured status filter. If
        `end_status` is None this returns the single start_status value,
        otherwise it returns a range like '200-299'.
        """
        return str(self.start_status) if self.end_status is None else f'{self.start_status}-{self.end_status}'

    def timestamp_filter(self, timestamp: int):
        """Return True if given timestamp is within configured [start, end].

        Treats a None `start` or `end` as an open bound.
        """
        return bool(
            (not self.start or timestamp >= self.start)
            and (not self.end or timestamp <= self.end)
        )
    
    def filter_status_code(self, code: int):
        """Return True if numeric status `code` is within configured bounds.

        Args:
            code: HTTP status code to test.

        Returns:
            True when code is >= start_status (if set) and <= end_status (if set).

        Notes:
            If `start_status` or `end_status` is None the corresponding bound
            is considered open.
        """
        return bool(
            (not self.start_status or self.start_status<=code)
            and (not self.end_status or self.end_status>=code)
        )
    
    def __str__(self):
        return ("<FilterOpt "
                f"top = {self.top} "
                f"start = {self.start} "
                f"end = {self.end} "
                f"method = {self.method} "
                f"start_status = {self.start_status} "
                f"end_status = {self.end_status}>"
        )
    
    __repr__ = __str__


default_filter = FilterOpt(3, None, None, None, 200, 520)