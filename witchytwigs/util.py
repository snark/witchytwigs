import full_yaml_metadata
import glob
import jinja2
import markdown
import os

md = markdown.Markdown(extensions=['full_yaml_metadata'])

def parse_entity_filename(entity_filename):
    path = os.path.split(entity_filename)
    etype = os.path.split(path[0])[1]
    filename, extension = os.path.splitext(path[-1])
    return filename, etype


def load_entities(entities_dir):
    # TODO:
    # This currently assumes a flat hierarchy solely of the form
    # entites_dir/type/name.md.
    entities = {}
    for entity in glob.iglob(entities_dir + '/**/*.md', recursive=True):
        with open(entity) as f:
            html = md.convert(f.read())
            name, entity_type = parse_entity_filename(entity)
            meta = md.Meta
            if html:
                meta['content'] = html
            else:
                meta['content'] = None
            # Allow overrides
            if 'name' not in meta:
                meta['name'] = name
            if 'type' not in meta:
                meta['type'] = entity_type
            if meta['type'] not in entities:
                entities[meta['type']] = {}
            entities[meta['type']][name] = meta
    print(entities)
    return entities


def render_pages(pages_dir, entities, template_dir, output_dir):
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        #autoescape=jinja2.select_autoescape(['html'])
    )
    pages = []
    for type_ in entities:
        for entity in entities[type_]:
            if entities[type_][entity].get('render'):
                # TODO: Unimplemented
                pass
    for page in glob.iglob(pages_dir + '/*.md'):
        with open(page) as f:
            html = md.convert(f.read())
            meta = md.Meta
            if not meta:
                meta = {}
            name, _ = parse_entity_filename(page)
            if 'name' in meta:
                name = meta['name']
            template_wanted = meta.get('template', 'default')
            template = template_env.get_template(
                template_wanted + '.html'
            )
            result = template.render(
                content=html,
                name=name,
                entities=entities,
                page=meta,
            )
            if meta.get('filename'):
                outname = meta['filename']
            else:
                outname = name + '.html'
            target = os.path.join(output_dir, outname)
            try:
                os.makedirs(
                    os.path.dirname(target)
                )
            except FileExistsError:
                pass
            with open(target, 'w') as f:
                f.write(result)


def build_pages(pages, entities, template_dir, output_dir):
    pass


def generate(site_dir, output_dir):
    entities_dir = os.path.join(site_dir, 'entities')
    pages_dir = os.path.join(site_dir, 'pages')
    template_dir = os.path.join(site_dir, 'templates')
    static_dir = os.path.join(site_dir, 'static')
    entities = load_entities(entities_dir)
    pages = render_pages(pages_dir, entities, template_dir, output_dir)
    #build_pages(pages, entities, template_dir, output_dir)
