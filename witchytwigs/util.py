import full_yaml_metadata
import glob
import jinja2
import markdown
from operator import itemgetter
import os
import shutil

md = markdown.Markdown(extensions=['full_yaml_metadata', 'markdown.extensions.smarty'])

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
            for k, v in meta.items():
                # These are layout elements, not text
                if k.endswith('_md'):
                    converted = md.convert(v.strip())
                    if converted.startswith('<p>'):
                        converted = converted[3:]
                    if converted.endswith('</p>'):
                        converted = converted[:-4]
                    meta[k[0:-3]] = converted
                    del(meta[k])
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
    return entities


def fallbackkeysort(value, attribute='', reverse=False):
    attrs = list(map(str.strip, attribute.split(',')))
    def sortfn(i):
        for key in attrs:
            if key in i.keys():
                return i[key]
        return ''
    return sorted(value, key=sortfn, reverse=reverse)


def render_pages(pages_dir, entities, template_dir, output_dir):
    # TODO: This and render_entities should have less duplicative code
    # so that, e.g., they can both use the same checks for render_with
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        #autoescape=jinja2.select_autoescape(['html'])
    )
    template_env.filters['fallbackkeysort'] = fallbackkeysort

    pages = []
    for type_ in entities:
        for entity in entities[type_]:
            e = entities[type_][entity]
            if e.get('use_entity'):
                source_entity = e.get('use_entity').split('/')
                if len(source_entity) != 2:
                    raise Exception(
                        'use_entity should be formatted as '
                        'type/entity_id in {}/{}'.format(type_, entity)
                    )
                source_type = source_entity[0]
                source_id = source_entity[1]
                try:
                    source = entities[source_type][source_id]
                    for k, v in source.items():
                        if k not in e.keys():
                            e[k] = v
                except KeyError:
                    raise Exception('Unknown entity {} in {}/{}'.format(
                        e.get('use_entity'),
                        type_,
                        entity
                    )) from None
            if e.get('render'):
                try:
                    render_with = e['render_with']
                except KeyError:
                    render_with = e.get('subtype', 'default')
                template = template_env.get_template(
                    render_with + '.html'
                )
                result = template.render(
                    content=e.get("content"),
                    entity=e,
                    page=e,
                )
                if e.get('render_to'):
                    target = os.path.join(
                        output_dir,
                        e['render_to'],
                        'index.html',
                    )
                else:
                    target = os.path.join(
                        output_dir,
                        type_,
                        e['name'],
                        'index.html'
                    )
                try:
                    os.makedirs(
                        os.path.dirname(target)
                    )
                except FileExistsError:
                    pass
                with open(target, 'w') as outfile:
                    outfile.write(result)
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
                outname = name
            if outname == "index":
                target = os.path.join(output_dir, "index.html")
            else:
                target = os.path.join(output_dir, outname, "index.html")
            try:
                os.makedirs(
                    os.path.dirname(target)
                )
            except FileExistsError:
                pass
            with open(target, 'w') as outfile:
                outfile.write(result)


def build_pages(pages, entities, template_dir, output_dir):
    pass


def copydir(source, dest):
    """Copy a directory structure overwriting existing files"""
    for root, dirs, files in os.walk(source):
        if not os.path.isdir(root):
            os.makedirs(root)
        for each_file in files:
            rel_path = root.replace(source, '').lstrip(os.sep)
            dest_path = os.path.join(dest, rel_path, each_file)
            try:
                os.makedirs(
                        os.path.dirname(dest_path)
                )
            except FileExistsError:
                pass
            shutil.copyfile(os.path.join(root, each_file), dest_path)


def generate(site_dir, output_dir):
    assets_dir = os.path.join(site_dir, 'assets')
    entities_dir = os.path.join(site_dir, 'entities')
    pages_dir = os.path.join(site_dir, 'pages')
    template_dir = os.path.join(site_dir, 'templates')
    static_dir = os.path.join(site_dir, 'static')
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    copydir(assets_dir, output_dir)
    entities = load_entities(entities_dir)
    pages = render_pages(pages_dir, entities, template_dir, output_dir)
