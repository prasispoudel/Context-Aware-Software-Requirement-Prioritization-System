// AppContext definition for use with React Context API (no export statement)

const AppContext = React.createContext();
window.AppContext = AppContext; // Expose globally for Babel/UMD usage