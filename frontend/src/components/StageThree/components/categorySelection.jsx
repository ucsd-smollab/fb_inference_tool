import styles from "../StageThreeStepThree.module.css"

const CategorySelection = (props) => {
  const changeCat = (events) => {
    props.changeCategory(props.category)
  }
  return (
    <div className={styles.CategoryListItem}>
      <button
        className={styles.CategoryListItemContainer}
        onClick={changeCat}
        style={{
          "backgroundColor": props.category===props.selectedCategory ? "lightBlue" : "white",
        }}
      >
        <h2>{props.category}</h2>
      </button>
    </div>
  );
};

export default CategorySelection;