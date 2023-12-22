// @ts-nocheck
import Card from "./Card";

// Defines a generalized modal used 
// throughout the application
function Modal(props) {
  // Concatenate the provided className with the base 'modal' class
  let modal = "fixed top-1/5 w-[40rem] p-4 rounded-lg shadow-xl z-30 animate-slide-down "
  let modalCSS = modal + props.className;

  const handleModalContentClick = (event) => {
    event.stopPropagation();
  };


  return (
    // Render a Card component to create the backdrop of the modal
    <Card onSaveClick={props.onSaveClick} className="fixed top-0 left-0 w-full h-screen z-20 bg-white bg-opacity-50 rounded-none flex justify-center">
      {/* Render a div element with the provided className to display the modal */}
      <div onClick={handleModalContentClick} className={modalCSS}>
        {/* Render the content of the modal */}
        {props.children}
      </div>
    </Card>
  );
}

export default Modal;
