import os
import subprocess



def list_sensors():
    """List all sensor simulator files in the current directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return [f for f in os.listdir(current_dir) if f.endswith('_sim.py')]

def run_sensor(sensor_file, processes):
    """Run a sensor simulator as a subprocess."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sensor_path = os.path.join(current_dir, sensor_file)
    process = subprocess.Popen(['python', sensor_path])
    processes[sensor_file] = process
    print(f"{sensor_file} is now running.")

def stop_sensor(sensor_file, processes):
    """Stop a running sensor simulator."""
    if sensor_file in processes:
        processes[sensor_file].terminate()
        processes[sensor_file].wait()
        del processes[sensor_file]
        print(f"{sensor_file} has been stopped.")

def show_status(processes, sensor_files):
    """Display the status of all sensors."""
    print("\nSensor Status:")
    for i, sensor in enumerate(sensor_files, start=1):
        status = "Running" if sensor in processes else "Stopped"
        print(f"{i}. {sensor}: {status}")

def interactive_control():
    """Interactive control for managing sensor simulators."""
    sensor_files = list_sensors()
    processes = {}

    while True:
        show_status(processes, sensor_files)
        print("\nEnter the number of a sensor to toggle its status, or 'q' to quit.")

        choice = input("Your choice: ")

        if choice.lower() == 'q':
            print("Exiting and stopping all sensors...")
            for sensor in list(processes.keys()):
                stop_sensor(sensor, processes)
            break

        if choice.isdigit():
            sensor_index = int(choice) - 1
            if 0 <= sensor_index < len(sensor_files):
                sensor_file = sensor_files[sensor_index]
                if sensor_file in processes:
                    stop_sensor(sensor_file, processes)
                else:
                    run_sensor(sensor_file, processes)
            else:
                print("Invalid sensor number. Please try again.")
        else:
            print("Invalid input. Please enter a number or 'q' to quit.")

if __name__ == "__main__":
    interactive_control()
