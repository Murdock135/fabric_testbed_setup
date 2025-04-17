ssh_command=$(python3 get_ssh_command.py)

if [ -z "$ssh_command" ]; then
    echo "No SSH command found."
    exit 1
fi
echo "Executing SSH command: $ssh_command"
eval "$ssh_command"

if [ $? -ne 0 ]; then
    echo "SSH command failed."
    exit 1
fi
echo "SSH command executed successfully."

