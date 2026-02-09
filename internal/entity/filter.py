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
        return str(self.start_status) if self.end_status==None else f'{self.start_status}-{self.end_status}'

    def timestamp_filter(self, timestamp: int):
        return bool(
            (not self.start or self.start>=timestamp)
            and (not self.end or self.end <= timestamp)
        )
    
    def filter_status_code(self, code: int):
        return bool(
            (not self.start_status or self.start_status>=code)
            and (not self.end_status or self.end_status <= code)
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


default_filter = FilterOpt(3, None, None, None, 200, 520)