// @ts-nocheck
import Modal from "../UI/Modal"
import Button from "../UI/Button"
function Login(props) {
  return (
    <Modal 
    onSaveLoginClick={props.onSaveLoginClick} 
    className={"bg-blue-600 flex flex-col items-center justify-center space-y-10 " + props.className}
    >
        <div className="flex-col space-y-4">
            <input 
                className="w-full rounded-full border-4 border-gray-300 py-2 px-4 text-gray-700 leading-tight 
                            focus:outline-none focus:bg-white focus:border-blue-500" 
                type="text" 
                placeholder="Enter Username" 
            />
            <input 
                className="w-full rounded-full border-4 border-gray-300 py-2 px-4 text-gray-700 leading-tight 
                            focus:outline-none focus:bg-white focus:border-blue-500" 
                type="password" 
                placeholder="Enter Password" 
            />
        </div>
    <Button outerClassname="bg-yellow-500" innerClassName="bg-yellow-400">Login</Button>
  </Modal>
  )
}

export default Login