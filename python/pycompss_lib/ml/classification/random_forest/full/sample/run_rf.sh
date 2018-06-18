#     --qos=debug \
#     --tracing=true \

enqueue_compss \
    --num_nodes=16 \
    --exec_time=30 \
    --cpus_per_node=48 \
    --worker_in_master_cpus=24 \
    --max_tasks_per_node=48 \
    --scheduler="es.bsc.compss.scheduler.fifoDataScheduler.FIFODataScheduler" \
    --worker_working_dir=scratch \
    ./main_random_forest.py \
        --path_in=/gpfs/projects/bsc19/COMPSs_DATASETS/random_forest/dt_test_3/ \
        --n_instances=100000 \
        --n_features=100 \
        --path_out=/gpfs/projects/bsc19/bsc19029/own_results/ \
        --n_estimators=10 \
        --max_depth=3 \