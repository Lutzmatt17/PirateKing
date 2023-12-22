// @ts-nocheck

function Button(props, outerClassname, innerClassName) {
  let bottomButton = "bg-red-700 rounded-lg border-none p-0 cursor-pointer outline-none w-44 " + outerClassname;
  let topButton = "block py-3 px-10 rounded-lg text-xl bg-red-600 text-black font-semibold transform active:-translate-y-px -translate-y-1.5 " + innerClassName;
  return (
    <button onClick={props.onClick} className={bottomButton}>
        <span className={topButton}>
            {props.children}
        </span>
    </button>
  )
}

export default Button