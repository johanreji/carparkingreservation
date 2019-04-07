from background_task import background

@background(schedule=60)
def sample_task():
	print("this is a background task")



sample_task(repeat=20)
