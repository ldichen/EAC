using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.Geometry;
using ESRI.ArcGIS.Display;
using ESRI.ArcGIS.Geodatabase;

namespace dataMatching
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void axLicenseControl1_Enter(object sender, EventArgs e)
        {

        }
        public static ISpatialReference GetSpatialRef(IFields fields)
        {
            IGeometryDef geometryDef = null;
            for (int i = 0; i < fields.FieldCount; i++)
            {
                IField field = fields.get_Field(i);
                if (field.Type == esriFieldType.esriFieldTypeGeometry)
                {
                    IFieldEdit fieldEdit = field as IFieldEdit;
                    geometryDef = fieldEdit.GeometryDef;
                    break;
                }
            }
            return geometryDef.SpatialReference;
        }
        private void startMatch_Click(object sender, EventArgs e)
        {
            IFeatureClass gdFeatCls =(axMapControl1.get_Layer(1) as IFeatureLayer).FeatureClass;//高德数据
            IFeatureClass osmFeatCls =(axMapControl1.get_Layer(0) as IFeatureLayer).FeatureClass;//0sM数据

            ISpatialReference spatialReference = GetSpatialRef(gdFeatCls.Fields);

            //OSM_GDMatching matching = new OSM_GDMatching(spatialReference);
            //matching.Excute(gdFeatCls, osmFeatCls);

            MNRelation mnRelation = new MNRelation();
            mnRelation.Excute(osmFeatCls);

            MessageBox.Show("完成!");
        }
    }
}
