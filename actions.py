import router
import response

actionRouter = router.Router()

def serve(data):
    try:
        return response.Response(
            200,
            open(data["location"], "rb").read(),
            data["extension"]
        )
    except IOError:
        return response.Response(
            int(data["defaultStatus"]),
            open(data["defaultLocation"], "rb").read(),
            data["defaultExtension"]
        )

def raw(data):
    return response.Response(int(data["status"]), data["data"].encode("utf8"), data["extension"])

actionRouter.actions = {
    "serve": serve,
    "raw": raw
}