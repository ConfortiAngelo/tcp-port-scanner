import asyncio
from core.models import PortStatus



async def connection(ip,port ,timeout):
    print("Comenzando...")
    try :
        reader , writer = await asyncio.wait_for(asyncio.open_connection(ip,port),timeout)
        print("Leyendo.....")   
        banner = await asyncio.wait_for(reader.read(1024),timeout)

        print(banner)

        #cierro la conexion
        writer.close()
        await writer.wait_closed()
        return PortStatus.OPEN        
    except ConnectionRefusedError:
        #definir como CLOSED
        print("closed")
        return PortStatus.CLOSED
    except TimeoutError:
        #definir como FILTERED
        print("filtered")
        return PortStatus.FILTERED

