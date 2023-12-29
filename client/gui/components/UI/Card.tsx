// Import necessary dependencies and styles
// @ts-nocheck

// Defines a generalized card component that
// is used throughout the application
function Card(props) {
  // Concatenate the provided className with the base 'card' class
  let card = "p-4 shadow-md rounded-lg "
  let cardCSS = card + props.className;
  
  const backgroundClickHandler = () => {
    if (props.onSavePlayClick) {
      props.onSavePlayClick(false);
    } else {
      props.onSaveLoginClick(false);
    }
  }
  return (
    // Render a div element with the provided className
    <div onClick={backgroundClickHandler} className={cardCSS}>
      {/* Render the content of the card */}
      {props.children}
    </div>
  );
}

export default Card;