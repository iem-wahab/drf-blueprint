from urllib.parse import parse_qs
from urllib.parse import urlparse

from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from drf_starter_template.utils.pagination import CustomDRFPagination


class CustomDRFPaginationTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_first_page_pagination(self):
        data = list(range(1, 26))
        request = self.factory.get("/items/?page=1")
        drf_request = Request(request)
        paginator = CustomDRFPagination()
        paginator.request = drf_request

        page = paginator.paginate_queryset(data, drf_request, view=None)
        response = paginator.get_paginated_response(page)

        meta = response.data.get("meta", {})
        assert meta.get("totalItems") == 25
        assert meta.get("pageSize") == 10
        assert meta.get("currentPage") == 1
        assert meta.get("totalPages") == 3

        links = response.data.get("links", {})
        assert "self" in links
        assert "first" in links
        assert "last" in links
        assert "next" in links
        assert "previous" in links

        assert links.get("previous") is None
        parsed_next = urlparse(links.get("next"))
        next_params = parse_qs(parsed_next.query)
        assert next_params.get("page") == ["2"]

    def test_last_page_pagination(self):
        data = list(range(1, 26))
        request = self.factory.get("/items/?page=3")
        drf_request = Request(request)
        paginator = CustomDRFPagination()
        paginator.request = drf_request

        page = paginator.paginate_queryset(data, drf_request, view=None)
        response = paginator.get_paginated_response(page)

        meta = response.data.get("meta", {})
        assert meta.get("currentPage") == 3
        assert meta.get("totalPages") == 3
        assert meta.get("totalItems") == 25
        assert meta.get("pageSize") == 10

        links = response.data.get("links", {})
        assert links.get("next") is None
        parsed_prev = urlparse(links.get("previous"))
        prev_params = parse_qs(parsed_prev.query)
        assert prev_params.get("page") == ["2"]

    def test_default_page_when_no_query_param(self):
        data = list(range(1, 26))
        request = self.factory.get("/items/")
        drf_request = Request(request)
        paginator = CustomDRFPagination()
        paginator.request = drf_request

        page = paginator.paginate_queryset(data, drf_request, view=None)
        response = paginator.get_paginated_response(page)

        meta = response.data.get("meta", {})
        assert meta.get("currentPage") == 1

    def test_build_page_url_preserves_query_params(self):
        request = self.factory.get("/items/?search=foo&page=2")
        drf_request = Request(request)
        paginator = CustomDRFPagination()
        paginator.request = drf_request

        url = paginator._build_page_url(1)  # noqa: SLF001
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        assert query_params.get("search") == ["foo"]
        assert query_params.get("page") == ["1"]

    def test_custom_page_size(self):
        data = list(range(1, 26))
        request = self.factory.get("/items/?page=1&page_size=5")
        drf_request = Request(request)
        paginator = CustomDRFPagination()
        paginator.request = drf_request

        page = paginator.paginate_queryset(data, drf_request, view=None)
        response = paginator.get_paginated_response(page)
        meta = response.data.get("meta", {})

        assert meta.get("totalItems") == 25
        assert meta.get("pageSize") == 5
        assert meta.get("currentPage") == 1
        assert meta.get("totalPages") == 5

    def test_max_page_size(self):
        data = list(range(1, 26))
        request = self.factory.get("/items/?page=1&page_size=1000")
        drf_request = Request(request)
        paginator = CustomDRFPagination()
        paginator.request = drf_request

        page = paginator.paginate_queryset(data, drf_request, view=None)
        response = paginator.get_paginated_response(page)
        meta = response.data.get("meta", {})

        assert meta.get("totalItems") == 25
        assert meta.get("pageSize") == 100
        assert meta.get("currentPage") == 1
        assert meta.get("totalPages") == 1

    def test_page_zero_and_negative(self):
        data = list(range(1, 26))
        request_zero = self.factory.get("/items/?page=0")
        drf_request_zero = Request(request_zero)
        paginator_zero = CustomDRFPagination()
        paginator_zero.request = drf_request_zero

        page_zero = paginator_zero.paginate_queryset(data, drf_request_zero, view=None)
        response_zero = paginator_zero.get_paginated_response(page_zero)
        meta_zero = response_zero.data.get("meta", {})
        assert meta_zero.get("currentPage") == 1

        request_neg = self.factory.get("/items/?page=-5")
        drf_request_neg = Request(request_neg)
        paginator_neg = CustomDRFPagination()
        paginator_neg.request = drf_request_neg

        page_neg = paginator_neg.paginate_queryset(data, drf_request_neg, view=None)
        response_neg = paginator_neg.get_paginated_response(page_neg)
        meta_neg = response_neg.data.get("meta", {})
        assert meta_neg.get("currentPage") == 1
