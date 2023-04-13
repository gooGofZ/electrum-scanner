import multiprocessing

def process_seed_phrase_con(start, end):
    
    # TODO: ถ้าจะนำไปใช้ ต้องแก้ไข้เส้นทางเป็นของตัวเองนะ wallet_path: ตรงนี้เรากำหนดเองว่าต้องการบันทึก account_{i}.json ที่ไหน
    mkdir = '/home/rushmi0/.electrum/electrum_wallet/'
    os.makedirs(mkdir, exist_ok=True)
    
    for index, seed_phrase in enumerate(brute_force()):
            # print(f'{index + 1} | {seed_phrase}')
            wallet_path = mkdir + f"account_{index}.json"
            executor.submit(
                 process_seed_phrase,
                 seed_phrase,
                 index,
                 target,
                 wallet_path
             )
           
            """
            future = executor.submit(
                process_seed_phrase,
                seed_phrase, index,
                target,
                wallet_path + f"/account_{index}.json"
            )

            if future.result() == "break":
                break
            """

if __name__ == '__main__':
    num_processes = multiprocessing.cpu_count()
    print(num_processes)
    pool = multiprocessing.Pool(processes=num_processes)


    # creating enumerate objects
    word_list = enumerate(["eat", "sleep", "repeat","eat", "sleep", "repeat","eat", "sleep", "repeat","eat", "sleep", "repeat"])
    
    start = 0
    # end = 10000000
    end = len(list(word_list))

    # Split the loop into chunks for each process
    chunk_size = int((end - start) / num_processes)
    chunks = [(i, i + chunk_size) for i in range(start, end, chunk_size)]

    # Run the loop in parallel using all the available CPUs
    pool.starmap(my_func, chunks)
   