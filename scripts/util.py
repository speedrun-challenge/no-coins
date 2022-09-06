# -*- coding: utf-8 -*-
import datetime


def is_before_deadline(d_str: str) -> bool:
  deadline = datetime.datetime.strptime("2022-09-05T03:00:00Z",
                                        "%Y-%m-%dT%H:%M:%SZ")
  d = datetime.datetime.strptime(d_str, "%Y-%m-%dT%H:%M:%SZ")
  return d < deadline
