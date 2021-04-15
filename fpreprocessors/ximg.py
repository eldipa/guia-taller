from typing import Dict
OptionValue = int or float or bool or str

from foliant.preprocessors.base import BasePreprocessor

class Preprocessor(BasePreprocessor):
    ''' Make the inclusion of images easier.

        <x-img src="!path image/path/img.png">
        Caption (optional)
        </x-img>
    '''
    tags = ('x-img',)

    def _process_img(self, tag: str, options: Dict[str, OptionValue], body: str) -> str:
        self.logger.debug(f'Processing img: {tag}, {options}, {body}')

        caption = body
        img_path = options['src']

        img_ref = f'![{caption}]({img_path})'

        return img_ref


    def process_imgs(self, content: str) -> str:
        def _sub(diagram) -> str:
            return self._process_img(
                diagram.group('tag'),
                self.get_options(diagram.group('options')),
                diagram.group('body')
            )

        return self.pattern.sub(_sub, content)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('ximg')
        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

    def apply(self):
        self.logger.info('Applying preprocessor.')

        for markdown_file_path in self.working_dir.rglob('*.md'):
            with open(markdown_file_path, encoding='utf8') as markdown_file:
                content = markdown_file.read()

            processed_content = self.process_imgs(content)

            if processed_content:
                with open(markdown_file_path, 'w', encoding='utf8') as markdown_file:
                    markdown_file.write(processed_content)

        self.logger.info('Preprocessor applied.')
