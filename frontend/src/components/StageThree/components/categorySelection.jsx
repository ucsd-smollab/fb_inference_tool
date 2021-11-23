import styles from "../StageThreeStepThree.module.css"

const CategorySelection = (props) => {
  const changeCat = (events) => {
    props.changeCategory(props.category)
  }
  return (
    <div className={styles.CategoryListContainer}>
      <button
        className={styles.CategoryListItem}
        onClick={changeCat}
        style={{
          "backgroundColor": props.category===props.selectedCategory ? "rgb(189, 231 , 255)" : 'rgb(240, 242, 245)',
        }}
      >
        <h3 style={{"marginBottom": "25px"}}>{props.category}</h3>
      </button>
    </div>
  );
};

export default CategorySelection;