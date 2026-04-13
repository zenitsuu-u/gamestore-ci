import pytest


@pytest.fixture(autouse=True)
def screenshot_on_fail(page, request):
     yield
     if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
         import os
         os.makedirs('screenshots', exist_ok=True)
         page.screenshot(path=f'screenshots/{request.node.name}.png')