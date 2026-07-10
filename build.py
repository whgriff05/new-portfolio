#!/usr/bin/env python3

"""

build.py - a static TOML website builder

Author: Will Griffin (https://github.com/whgriff05)

"""


# Imports
import jinja2
import markdown
import pathlib
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn
import sys
import time
import tomllib


# Page Class
class Page:
    Template = """{{% extends "base.html" %}}
    {{% block main %}}
    {}
    {{% endblock main %}}
    """

    def __init__(self, path, title, navigation, body, **kwargs):
        self.path = path                    # Page path (path to page.toml AND URL path)
        self.title = title                  # Page title 
        self.navigation = navigation        # Page navigation links
        self.body = body                    # Page body
        self.kwargs = kwargs                # Page variables

    def __str__(self):
        return f"<Page {self.title}: {self.navigation} | {self.kwargs}> ({self.path})"

    def __repr__(self):
        return str(self)

    @classmethod
    def load_page(cls, path):
        with path.open(mode="rb") as page_fp:
            # Read/parse the TOML data
            toml_data = tomllib.load(page_fp)

            # Check if all necessary fields exist
            if (
                    "page" not in toml_data or
                    "title" not in toml_data["page"] or
                    "navigation" not in toml_data["page"] or
                    
                    "content" not in toml_data or
                    "body" not in toml_data["content"]
                    ):
                print(f"Error: field missing from {path}", file=sys.stderr)
                sys.exit(1)

            # Create the page object
            page_path = str(path).split("/")
            page_path[0] = "public"
            page_path = "/".join(page_path)
            page_path = pathlib.Path(page_path.replace(".toml", ".html"))
            page_kwargs = {k: v for k, v in toml_data["page"].items() if k not in {"title", "navigation"}}
            page = cls(page_path, toml_data["page"]["title"], toml_data["page"]["navigation"], toml_data["content"]["body"], **page_kwargs)

            return page

    def build(self, site):
        body = markdown.markdown(self.body, extensions=["fenced_code", "codehilite"])
        env = jinja2.Environment(
                loader = jinja2.FileSystemLoader(site.templates_path),
                trim_blocks = True,
                )
        template = env.from_string(self.Template.format(body))
        settings = {
                "site": site,
                "page": self,
                }
        return template.render(**settings)

class Site:
    def __init__(self, title, base_path, templates_path, output_path):
        self.title = title                      # Site title
        self.pages = []                         # Site pages
        self.base_path = base_path              # Site builder base path
        self.templates_path = templates_path    # Site templates path
        self.output_path = output_path          # Site builder output path

    @classmethod
    def build_site_class(cls, path, base_path):
        # Get index.toml file
        index = path / "index.toml"

        # Get the site title from the index.toml file
        with index.open(mode="rb") as index_fp:
            index_data = tomllib.load(index_fp)

            try:
                site_title = index_data["page"]["title"]
            except:
                print("Error: site title does not exist", file=sys.stderr)
                sys.exit(1)

        # Define the templates path and output path
        templates_path = base_path / "templates"
        output_path = base_path / "public"

        # Create the site object
        site = cls(site_title, base_path, templates_path, output_path)

        # Walk the directory tree, building pages out of each toml file
        progress = Progress(
                TextColumn("{task.description}"),
                BarColumn(),
                MofNCompleteColumn()
                )
        task_id = progress.add_task("Loading Pages", total=0)
        task = progress.tasks[task_id]
        progress.start()
        for walk_path, _, pages in path.walk():
            time.sleep(0.1)
            progress.update(task_id, total=(task.total or 0) + len(pages))
            for page_name in pages:
                if page_name.endswith(".toml"):
                    site.build_page_class(walk_path / page_name) 
                    progress.update(task_id, advance=1)
        progress.stop()


        return site

    def build_page_class(self, path):
        # Build and append page
        page = Page.load_page(path)
        self.pages.append(page)

    def build_site(self):
        # Make sure output path directory exists
        if not self.output_path.is_dir():
            self.output_path.mkdir(parents=True, exist_ok=True)

        progress = Progress(
                TextColumn("{task.description}"),
                BarColumn(),
                MofNCompleteColumn()
                )
        task_id = progress.add_task("Loading Pages", total=len(self.pages))

        progress.start()
        for page in self.pages:
            self.build_page(page)
            progress.update(task_id, advance=1)
            time.sleep(0.1)

        progress.stop()

    def build_page(self, page):
        # Make sure file path exists
        page.path.parent.mkdir(parents=True, exist_ok=True)

        with open(page.path, "w") as page_fp:
            page_fp.write(page.build(self))

# Main Function
def main(argc=len(sys.argv), argv=sys.argv):
    base_path = pathlib.Path(".")
    input_path = base_path / "site"

    index = input_path / "index.toml"
    if not index.exists():
        print("Error: index.toml does not exist", file=sys.stderr)
        sys.exit(1)

    site = Site.build_site_class(input_path, base_path)
    site.build_site()

if __name__ == "__main__":
    main()
