// @ts-nocheck

function Button(props) {
  let bottomButton = "rounded-lg border-none p-0 cursor-pointer outline-none " + props.outerClassname;
  let topButton = "block py-3 px-10 rounded-lg text-xl text-black font-semibold transform active:-translate-y-px -translate-y-1.5 " + props.innerClassName;
  return (
    <button onClick={props.onClick} className={bottomButton}>
        <span className={topButton}>
            {props.children}
        </span>
    </button>
  )
}

export default Button