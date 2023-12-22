// @ts-nocheck
import Modal from "../UI/Modal"

function Join(props) {

  return (
    <Modal onSaveClick={props.onSaveClick} className="bg-blue-600">
        <input 
            className="w-full rounded-full border-4 border-gray-300 py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500" 
            type="text" 
            placeholder="Enter Username" 
        />
    </Modal>
  )
}

export default Join;