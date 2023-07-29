set -e
su 
set -e
cd /data/data/com.xiaomi.hm.health/files/watch_skin_local/
dirs=( * )
cd ${dirs[0]}
dirs=( * )
cd ${dirs[0]}
files=( *.bin )
cp /data/local/tmp/miband5_packed.bin ${files[0]}
files=( *.png )
cp /data/local/tmp/miband5_packed_preview.png ${files[0]}
