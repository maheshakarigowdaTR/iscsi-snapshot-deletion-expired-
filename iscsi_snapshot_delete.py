import datetime
import requests
cluster_ips = ['eg-si-clbk-e01']
admin_creds = ("admin", "Thomson123")
def get_volumes(cluster_ip):
    r = requests.get(
        "http://{​}​/api/storage/volumes".format(cluster_ip),
        auth=admin_creds,
    )
    r.raise_for_status()
    return r.json().get("records")
def get_snapshots(cluster_ip, volume_uuid):
    r = requests.get(
        "http://{​}​/api/storage/volumes/{​}​/snapshots".format(cluster_ip, volume_uuid),
        auth=admin_creds,
    )
    r.raise_for_status()
    return r.json().get("records")
def get_snapshot_info(cluster_ip, volume_uuid, snapshot_uuid):
    r = requests.get(
        "http://{​}​/api/storage/volumes/{​}​/snapshots/{​}​".format(
            cluster_ip, volume_uuid, snapshot_uuid
        ),
        auth=admin_creds,
    )
    r.raise_for_status()
    return r.json()
def delete_snapshot(cluster_ip, volume_uuid, snapshot_uuid):
    r = requests.delete(
        "http://{​}​/api/storage/volumes/{​}​/snapshots/{​}​".format(cluster_ip, volume_uuid, snapshot_uuid),
        auth=admin_creds,
    )
    r.raise_for_status()
    return r.json()
def get_snapshot_retention_for_volume(volume_name) -> int:
    if "p_i_dbi_ritm" in volume_name:
        # naming pattern must resemble 'sv_aiid202271_p_i_dbi_ritm2585175_01_snap14'
        return int(volume_name.split("snap")[1])
    elif "_wi_" in volume_name:
        # naming pattern must resemble 'sv_07_cb0186_wi_uipathuat_1_info_snap'
        return int(volume_name.split("_")[1])
if __name__ == "__main__":
    current_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    for cluster_ip in cluster_ips:
        for volume in get_volumes(cluster_ip):
            volume_name = volume["name"]
            snapshot_retention = get_snapshot_retention_for_volume(volume_name)
            if snapshot_retention:
                print("{​}​ has a snapshot retention of {​}​.".format(volume_name, snapshot_retention))
                for snapshot in get_snapshots(cluster_ip, volume.get("uuid")):
                    snapshot_info = get_snapshot_info(
                        cluster_ip, volume.get("uuid"), snapshot.get("uuid")
                    )
                    snapshot["created_datetime"] = datetime.datetime.fromisoformat(
                        snapshot_info["create_time"]
                    ).replace(tzinfo=datetime.timezone.utc)
                    if (
                        current_time - snapshot["created_datetime"]
                    ) > datetime.timedelta(days=snapshot_retention):
                        print(deleting {​}​".format(snapshot["name"]))
                        delete_snapshot(cluster_ip, volume.get("uuid"), snapshot.get("uuid"))
