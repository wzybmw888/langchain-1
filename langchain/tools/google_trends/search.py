from enum import Enum
from typing import TYPE_CHECKING, Type, Optional

from pydantic import BaseModel, Field

from langchain.tools import BaseTool
from langchain.tools.google_trends.utils import mk_test, import_google_trend


class TrendSearchSchema(BaseModel):
    keyword: str = Field(
        ...,
        description="keyword information"
    )
    period: Optional[str] = Field(
        ...,
        example="today 3-m",
        description="contains start date, end date"
    )
    cat: Optional[int] = Field(
        default=0,
        description="Category of the industry where the information is queried"
    )
    geo: Optional[str] = Field(
        default="",
        description="Category of the country where the information is located"
    )


class GoogleTrendSearch(BaseTool):
    name: str = "google_trend_search"
    description: str = (
        "Use this tool to search related google trend with the provided message fields."
    )
    args_schema: Type[TrendSearchSchema] = TrendSearchSchema

    @staticmethod
    def _prepare_search(
            keyword: str,
            period: Optional[str] = "today 3-m",
            cat: Optional[str] = 0,
            geo: Optional[str] = ""
    ) -> str:
        TrendReq = import_google_trend()
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2, backoff_factor=0.1)
        pytrends.build_payload([keyword], cat=cat, timeframe=period, geo=geo, gprop='')
        trends_data = pytrends.interest_over_time()
        _tmp = trends_data[keyword]
        res = mk_test(_tmp)
        return res

    def _run(
            self,
            keyword: str,
            period: Optional[str] = "today 3-m",
            cat: Optional[str] = 0,
            geo: Optional[str] = ""
    ) -> str:
        """Run the tool."""
        results = self._prepare_search(keyword, period, cat, geo)
        return results

    async def _arun(
            self,
            keyword: str,
            period: str,
            cat: str,
            geo: str
    ) -> str:
        """Run the tool."""
        raise NotImplementedError(f"The tool {self.name} does not support async yet.")
