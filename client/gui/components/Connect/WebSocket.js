let socket;

export const initiateConnection = () => {
  if (!socket) {
    socket = new WebSocket('ws://192.168.86.34:8765')
  }

  return socket;
}

export const disconnectSocket = () => {
    if (socket) {
        socket.close()
        socket = null;
    }
}

export const getSocket = () => socket;
