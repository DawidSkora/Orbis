import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def _choose_supabase_key() -> str:
    """
    Prefer server-side keys (service_role) when present; otherwise anon.
    Avoid using sb_publishable_* which won't authorize PostgREST operations.
    """
    service = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    anon = os.environ.get("SUPABASE_ANON_KEY")
    fallback = os.environ.get("SUPABASE_KEY")

    chosen = service or anon or fallback
    if chosen and chosen.startswith("sb_publishable_") and (service or anon):
        chosen = service or anon
    return chosen  # type: ignore[return-value]

_chosen_key = _choose_supabase_key()

supabase: Client = create_client(
    os.environ["SUPABASE_URL"],
    _chosen_key
)