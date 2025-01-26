import instagramapi as instagrapi, asyncio, inspect
from instagramapi.types import DirectMessage as Message

client = instagrapi.Client()
client.login("kauliarikobot", "KaulasBotaki")
print("Logged in!")

allMessages: dict[int, list[int]] = {}
commands: list = []
ars: list = []
pprefix: str = "!"

targets: list = [] # To be replaced

class Command:

    container = commands

    def __init__(self, *names: str, callback, prefix: bool = True):

        fixedNames = []

        for name in names:
            fixedNames.append((pprefix if prefix else "") + str(name).lower().removeprefix(pprefix))
        
        self.names = fixedNames
        self.callback = callback
        self.description = callback.__doc__ or "❌ Den uparxei perigrafh gia authn thn entolh akoma"
        self.container.append(self)

class AR(Command):

    container = ars

    def __init__(self, *names: str, callback = None, response: str = None):

        if response is not None:

            async def custom(thread):
                await sendMessage(response, thread, True)

            callback = custom

        super().__init__(*names, callback=callback)

def command(*names: str):

    def decorator(callback):
        nonlocal names
        return Command(*names, callback=callback)

    return decorator

def ar(*names: str):

    def decorator(callback):
        nonlocal names
        return AR(*names, callback=callback)

    return decorator

def asyncify(function, task: bool = False):

    async def withThread(*args, **kwargs):
        nonlocal function
        return await asyncio.to_thread(function, *args, **kwargs)
    
    async def withTask(*args, **kwargs):
        nonlocal function
        return asyncio.create_task((function(*args, **kwargs) if inspect.iscoroutinefunction(function) else withThread(*args, **kwargs)))
    
    return withTask if task else withThread

async def sendMessage(content: str, target: int, task: bool = False):
    """🗣️ Lew oti goustareis px "pes me aggizei o theios mou\""""
    return await asyncify(client.direct_answer, task)(target, str(content))

async def sendImage(path: str, target: int, task: bool = False):
    """Send an image"""
    return await asyncify(client.direct_send_photo, task)(path, thread_ids=[target])

async def handleMessage(message: Message):

    content = message.text
    thread = message.thread_id

    if content is None or message.user_id == "71058424484":
        return
    
    for command in commands:

        epiloges = command.names

        for epilogh in epiloges:

            if content.lower().startswith(epilogh):

                song = content[len(epilogh):].strip()
                #await asyncify(client.direct_send_seen, True)(thread)
                return asyncio.create_task(command.callback(song, thread))

    for ar in ars:
        for name in ar.names:
            if name.lower() in content.lower():
                return asyncio.create_task(ar.callback(thread))

print(", ".join([thread.id for thread in client.direct_threads(0, thread_message_limit=0) if int(thread.id) not in targets]))

async def readMessages(target):
    latest = client.direct_messages(target)
    existing = allMessages.get(target)
    first = False

    if existing is None:
        existing, first = [], True

    new = [message for message in latest if message.id not in existing]
    existing.extend([message.id for message in new])
    allMessages[target] = existing

    if not first:
        await asyncio.gather(*[handleMessage(message) for message in new])

async def main():

    global targets
    print("Targets:", targets)
    
    if targets:
        await sendMessage("✅ To bot leitourgei!", targets[0])
    else:
        print("Den exeis valei kanena target")

    while True:
        coroutines = [readMessages(target) for target in targets]
        await asyncio.gather(*coroutines)

def run(*channels: int, prefix: str = "!"):

    global targets, pprefix

    if channels:
        targets = list(channels)
        
    asyncio.run(main())