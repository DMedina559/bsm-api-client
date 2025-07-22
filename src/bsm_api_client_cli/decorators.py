import asyncio
import functools
import click

class AsyncGroup(click.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.async_context_settings = {}

    def context(self, f):
        self.async_context_settings['context'] = f
        return f

    def invoke(self, ctx):
        ctx.obj = ctx.obj or {}
        if self.async_context_settings.get('context'):
            async def runner():
                async with self.async_context_settings['context'](ctx) as cm:
                    return await super(AsyncGroup, self).invoke(ctx)
            return asyncio.run(runner())
        return super().invoke(ctx)

def pass_async_context(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        ctx = click.get_current_context()
        return f(ctx, *args, **kwargs)
    return wrapper
