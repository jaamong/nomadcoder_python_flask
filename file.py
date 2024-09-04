def save_to_file(file_name, jobs):
    file = open(file=f"{file_name}.csv", mode="w", encoding="UTF-8", newline="")
    file.write("Title,Company,Reward,Link\n")

    for job in jobs:
        file.write(
            f"{job['title']}, {job['company']}, {job['reward']}, {job['link']}\n"
        )

    file.close()
