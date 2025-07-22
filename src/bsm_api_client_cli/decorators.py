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
                async with self.async_context_settings['context'](ctx):
                    result = super(AsyncGroup, self).invoke(ctx)
                    if asyncio.iscoroutine(result):
                        return await result
                    return result
            
            # If we are in an async context, we need to run the async runner
            # otherwise we can just run the sync runner.
            try:
                asyncio.get_running_loop()
                return runner()
            except RuntimeError:
                return asyncio.run(runner())
        
        result = super().invoke(ctx)
        if asyncio.iscoroutine(result):
            try:
                asyncio.get_running_loop()
                return result
            except RuntimeError:
                return asyncio.run(result)
        return result

def pass_async_context(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        ctx = click.get_current_context()
        return f(ctx, *args, **kwargs)
    return wrapper
