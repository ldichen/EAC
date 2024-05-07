using ESRI.ArcGIS.Geodatabase;
using ESRI.ArcGIS.Geometry;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Windows.Forms;
using ESRI.ArcGIS.DataSourcesGDB;

namespace dataMatching
{
    /// <summary>
    /// 刘迪宸 双向面积匹配算法，用于计算位置偏差和
    /// </summary>
    public class OSM_GDMatching
    {
        private ISpatialReference spatialReference;
        public OSM_GDMatching(ISpatialReference spatialReference)
        {
            this.spatialReference = spatialReference;
        }


        public static ITable OpenTable(IWorkspace2 workspace2, string tableName)
        {
            IFeatureWorkspace featureWorkspace = workspace2 as IFeatureWorkspace;
            IWorkspaceFactory2 workspaceFactory2 = new FileGDBWorkspaceFactoryClass();
            workspaceFactory2 = (workspace2 as IWorkspace).WorkspaceFactory as IWorkspaceFactory2;
            IWorkspaceFactoryLockControl workspaceFactoryLockControl = workspaceFactory2 as IWorkspaceFactoryLockControl;
            if (workspaceFactoryLockControl.SchemaLockingEnabled)
            {
                workspaceFactoryLockControl.DisableSchemaLocking();
            }
            ITable table = null;
            if (workspace2.get_NameExists(esriDatasetType.esriDTTable, tableName)) //存在该Table
            {
                table = featureWorkspace.OpenTable(tableName);
            }
            return table;
        }
        /// <summary>
        /// 双向面积重叠法
        /// </summary>
        /// <param name="sFeatCls">高德地图 gdFeatCls</param>
        /// <param name="tFeatCls">OSM数据 osmFeatCls</param>
        public void Excute(IFeatureClass gdFeatCls, IFeatureClass osmFeatCls)
        {
            IDataset dataset = (IDataset)gdFeatCls;
            IWorkspace workspace = dataset.Workspace as IWorkspace;
            IWorkspaceEdit workspaceEdit = workspace as IWorkspaceEdit;
            ITable resultTable = OpenTable(workspace as IWorkspace2, "res");//匹配结果表
            int iSource = resultTable.FindField("GD");
            int iTarget = resultTable.FindField("OSM");
            int iStepCount = resultTable.FindField("StepCount");
            int currentOid = -1;
            double th = 0.3;//双向面积

            int stepLength = 1000;
            int FeatCount = osmFeatCls.FeatureCount(null);
            int stepCount = FeatCount / stepLength;
            for (int i = 0; i <= stepCount; i++)
            {
                Console.WriteLine("当前步骤："+ i.ToString());
                int startOID = i * stepLength + 1;
                int endOID = (i + 1) * stepLength;
                if (i == stepCount)
                    endOID = FeatCount;
                //开始编辑     
                workspaceEdit.StartEditing(true);
                workspaceEdit.StartEditOperation();
                IRowBuffer rowBuffer = null;
                ICursor rowCursor = null;
                List<int> sRes = null;
                List<int> tRes = null;
                IFeature osmFeature = null;
                for (int j = startOID; j <= endOID; j++)
                {
                    try
                    {
                        osmFeature = osmFeatCls.GetFeature(j);
                        sRes = new List<int>();
                        tRes = new List<int>();
                        List<IFeature> sFeatures = new List<IFeature>();
                        List<IFeature> tFeatures = new List<IFeature>();
                        tFeatures.Add(osmFeature);
                        tRes.Add(osmFeature.OID);

                        //1、第一次，t去找s         
                        List<IFeature> sCanFeatures = new List<IFeature>();
                        ISpatialFilter spatialFilter = new SpatialFilterClass();
                        spatialFilter.SpatialRel = esriSpatialRelEnum.esriSpatialRelIntersects;
                        spatialFilter.Geometry = osmFeature.Shape;
                        IFeatureCursor sFeatCur = gdFeatCls.Search(spatialFilter, false);
                        IFeature sFeature = sFeatCur.NextFeature();
                        while (sFeature != null)
                        {
                            sCanFeatures.Add(sFeature);
                            sFeature = sFeatCur.NextFeature();
                        }
                     
                        //新找到的s
                        List<IFeature> sMatchedFeatures = this.GetMatchFeatures(tFeatures, sCanFeatures, th);
                        sFeatures = sMatchedFeatures;
                        for (int m = 0; m < sFeatures.Count; m++)
                        {
                            sRes.Add(sFeatures[m].OID);
                        }

                        //if (sFeatures != null) Marshal.ReleaseComObject(sFeatures);
                        //if (tFeatures != null) Marshal.ReleaseComObject(tFeatures);
                        //if (sCanFeatures != null) Marshal.ReleaseComObject(sCanFeatures);
                        //if (sMatchedFeatures != null) Marshal.ReleaseComObject(sMatchedFeatures);

                        if (sFeatCur != null) Marshal.ReleaseComObject(sFeatCur);
                        if (spatialFilter != null) Marshal.ReleaseComObject(spatialFilter);
                        if (sFeature != null) Marshal.ReleaseComObject(sFeature);

                        //将匹配结果存入表中
                        if (sRes.Count == 0)
                        {
                            rowBuffer = resultTable.CreateRowBuffer();
                            rowCursor = resultTable.Insert(true);
                            rowBuffer.set_Value(iSource, -1);
                            rowBuffer.set_Value(iTarget, osmFeature.OID); 
                            rowBuffer.set_Value(iStepCount, i);
                            rowCursor.InsertRow(rowBuffer);
                        }
                        else
                        {
                            rowBuffer = resultTable.CreateRowBuffer();
                            rowCursor = resultTable.Insert(true);
                            rowBuffer.set_Value(iSource, this.GetOIDsText(sRes));
                            rowBuffer.set_Value(iTarget, this.GetOIDsText(tRes));
                            rowBuffer.set_Value(iStepCount, i);
                            rowCursor.InsertRow(rowBuffer);
                        }
                    }
                    catch
                    {
                        currentOid = osmFeature.OID;
                        Console.WriteLine("未匹配OID：" + currentOid.ToString());
                    }
                }
                rowCursor.Flush();
                workspaceEdit.StopEditOperation();
                workspaceEdit.StopEditing(true);

                if (osmFeature != null) Marshal.ReleaseComObject(osmFeature);
                //if (sRes != null) Marshal.ReleaseComObject(sRes);
                //if (tRes != null) Marshal.ReleaseComObject(tRes);
                if (rowBuffer != null) Marshal.ReleaseComObject(rowBuffer);
                if (rowCursor != null) Marshal.ReleaseComObject(rowCursor);
                //if (workspaceEdit != null) Marshal.ReleaseComObject(workspaceEdit);
            }
            MessageBox.Show("匹配结束,耗时：");
        }

        /// <summary>
        /// 双向面积重叠法
        /// </summary>
        /// <param name="tFeature">开始查找的要素</param>
        /// <param name="sFeatCls">源要素集</param>
        /// <param name="tFeatCls">目标要素集</param>
        /// <returns></returns>
        private void TWAO(IFeature tFeature, IFeatureClass sFeatCls, IFeatureClass tFeatCls, out List<int> sRes, out List<int> tRes)
        {

            double th = 0.3;//双向面积
            sRes = new List<int>();
            tRes = new List<int>();
            List<IFeature> sFeatures = new List<IFeature>();
            List<IFeature> tFeatures = new List<IFeature>();
            tFeatures.Add(tFeature);
            tRes.Add(tFeature.OID);

            //1、第一次，t去找s         
            List<IFeature> sCanFeatures = new List<IFeature>();
            ISpatialFilter spatialFilter = new SpatialFilterClass();
            spatialFilter.SpatialRel = esriSpatialRelEnum.esriSpatialRelIntersects;
            spatialFilter.Geometry = tFeature.Shape;
            IFeatureCursor sFeatCur = sFeatCls.Search(spatialFilter, false);
            IFeature sFeature = sFeatCur.NextFeature();
            while (sFeature != null)
            {
                sCanFeatures.Add(sFeature);
                sFeature = sFeatCur.NextFeature();
            }
            if (sFeatCur != null) Marshal.ReleaseComObject(sFeatCur);
            //新找到的s
            List<IFeature> sMatchedFeatures = this.GetMatchFeatures(tFeatures, sCanFeatures, th);
            sFeatures = sMatchedFeatures;
            for (int i = 0; i < sFeatures.Count; i++)
            {
                sRes.Add(sFeatures[i].OID);
            }

            //2、第二次，反向匹配,通过找到的s去找t
            if (sFeatures.Count > 0)
            {
                IFeatureCursor tFeatCur2 = null;
                IFeature tFeature2 = null;
                List<IFeature> tCanFeatures = new List<IFeature>();
                for (int i = 0; i < sFeatures.Count; i++)
                {
                    spatialFilter.Geometry = sFeatures[i].Shape;
                    tFeatCur2 = tFeatCls.Search(spatialFilter, false);
                    tFeature2 = tFeatCur2.NextFeature();
                    while (tFeature2 != null)
                    {
                        if (!tRes.Contains(tFeature2.OID))
                        {
                            tCanFeatures.Add(tFeature2);//待确认的新增T要素
                        }
                        tFeature2 = tFeatCur2.NextFeature();
                    }
                }
                if (tFeatCur2 != null) Marshal.ReleaseComObject(tFeatCur2);
                //新找到的t
                List<IFeature> tMatchedFeatures = this.GetMatchFeatures(sFeatures, tCanFeatures, th);
                for (int i = 0; i < tMatchedFeatures.Count; i++)
                {
                    tFeatures.Add(tMatchedFeatures[i]);
                    tRes.Add(tMatchedFeatures[i].OID);
                }

                //3、第三次，再通过找到的t去找s
                if (tMatchedFeatures.Count > 0)
                {
                    IFeatureCursor sFeatCur3 = null;
                    IFeature tFeature3 = null;
                    IFeature sFeature3 = null;
                    sCanFeatures = new List<IFeature>();
                    for (int i = 0; i < tMatchedFeatures.Count; i++)
                    {
                        tFeature3 = tMatchedFeatures[i];
                        spatialFilter.Geometry = tFeature3.Shape;
                        sFeatCur3 = sFeatCls.Search(spatialFilter, false);
                        sFeature3 = sFeatCur3.NextFeature();
                        while (sFeature3 != null)
                        {
                            if (!sRes.Contains(sFeature3.OID))
                            {
                                sCanFeatures.Add(sFeature3);
                            }
                            sFeature3 = sFeatCur3.NextFeature();
                        }
                    }
                    if (sFeatCur3 != null) Marshal.ReleaseComObject(sFeatCur3);
                    sMatchedFeatures = this.GetMatchFeatures(tFeatures, sCanFeatures, th);
                    for (int i = 0; i < sMatchedFeatures.Count; i++)
                    {
                        sFeatures.Add(sMatchedFeatures[i]);
                        sRes.Add(sMatchedFeatures[i].OID);
                    }

                    //4、第四次，再通过找到的s去找t
                    if (sMatchedFeatures.Count > 0)
                    {
                        IFeatureCursor tFeatCur4 = null;
                        IFeature tFeature4 = null;
                        IFeature sFeature4 = null;
                        tCanFeatures = new List<IFeature>();
                        for (int i = 0; i < sMatchedFeatures.Count; i++)
                        {
                            sFeature4 = sMatchedFeatures[i];
                            spatialFilter.Geometry = sFeature4.Shape;
                            tFeatCur4 = tFeatCls.Search(spatialFilter, false);
                            tFeature4 = tFeatCur4.NextFeature();
                            while (tFeature4 != null)
                            {
                                if (!tRes.Contains(tFeature4.OID))
                                {
                                    tCanFeatures.Add(tFeature4);
                                }
                                tFeature4 = tFeatCur4.NextFeature();
                            }
                        }
                        if (tFeatCur4 != null) Marshal.ReleaseComObject(tFeatCur4);
                        tMatchedFeatures = this.GetMatchFeatures(sFeatures, tCanFeatures, th);
                        for (int i = 0; i < tMatchedFeatures.Count; i++)
                        {
                            tFeatures.Add(tMatchedFeatures[i]);
                            tRes.Add(tMatchedFeatures[i].OID);
                        }
                    }
                }
            }
            if (spatialFilter != null) Marshal.ReleaseComObject(spatialFilter);
        }

        /// <summary>
        /// 通过TWAO算法获取M:N
        /// </summary>
        /// <param name="features">已经确定的要素</param>
        /// <param name="mFeatures">新增的要素，与features待匹配的要素</param>
        /// <param name="th">重叠面积阈值</param>
        /// <returns>匹配的结果</returns>
        private List<IFeature> GetMatchFeatures(List<IFeature> features, List<IFeature> mFeatures, double th)
        {
            List<IFeature> checkMFeatures = new List<IFeature>();
            string relationDescription = "RELATE(G1, G2, 'T********')";
            IPolygon mPolygon = null;
            IPolygon polygon = null;
            IGeometry newGeometry = null;
            IPolygon newPolygon = null;
            for (int i = 0; i < mFeatures.Count; i++)
            {
                mPolygon = mFeatures[i].Shape as IPolygon;
                mPolygon.SpatialReference = this.spatialReference;
                ITopologicalOperator2 topologicalOperator = (mPolygon as ITopologicalOperator2);
                topologicalOperator.IsKnownSimple_2 = false;
                topologicalOperator.Simplify();
                double sArea = Math.Abs((mPolygon as IArea).Area);

                double sumOverlapArea = 0;//重叠面积
                double tSumArea = 0;//发生重叠的要素总面积
                for (int j = 0; j < features.Count; j++)
                {
                    polygon = features[j].Shape as IPolygon;
                    polygon.SpatialReference = this.spatialReference;
                    bool isIntersects = (mPolygon as IRelationalOperator).Relation(polygon, relationDescription);
                    if (isIntersects)
                    {
                        tSumArea += Math.Abs((polygon as IArea).Area);
                        newGeometry = topologicalOperator.Intersect(polygon, esriGeometryDimension.esriGeometry2Dimension);
                        if (newGeometry != null && !newGeometry.IsEmpty)
                        {
                            newGeometry.SpatialReference = this.spatialReference;
                            newPolygon = newGeometry as IPolygon;
                            double overlapArea = Math.Abs((newPolygon as IArea).Area);
                            sumOverlapArea += overlapArea;
                        }
                    }
                }
                //开始判断
                double overlapRatio = sumOverlapArea / Math.Min(sArea, tSumArea);
                if (overlapRatio > th)
                {
                    checkMFeatures.Add(mFeatures[i]);
                }
            }
            //if (mPolygon != null) Marshal.ReleaseComObject(mPolygon);
            //if (polygon != null) Marshal.ReleaseComObject(polygon);
            if (newGeometry != null) Marshal.ReleaseComObject(newGeometry);
            if (newPolygon != null) Marshal.ReleaseComObject(newPolygon);

            return checkMFeatures;
        }

        /// <summary>
        /// OID合并为字符，去除重复
        /// </summary>
        /// <param name="sOIDs"></param>
        /// <returns></returns>
        public string GetOIDsText(List<int> sOIDs)
        {
            if (sOIDs == null)
            {
                return "";
            }
            string result = "";
            List<int> lst = new List<int>();
            for (int i = 0; i < sOIDs.Count; i++)
            {
                if (!lst.Contains(sOIDs[i]))
                {
                    lst.Add(sOIDs[i]);
                    result = result + sOIDs[i] + ",";
                }
            }
            if (result != "")
            {
                result = result.Substring(0, result.Length - 1);
            }
            return result;
        }

        private List<int> QueryFeatures(IGeometry geometry, IFeatureClass featureClass)
        {
            List<int> OIDs = new List<int>();
            ISpatialFilter spatialFilter = new SpatialFilterClass();
            spatialFilter.SpatialRel = esriSpatialRelEnum.esriSpatialRelIntersects;
            spatialFilter.Geometry = geometry;
            IFeatureCursor featureCursor = featureClass.Search(spatialFilter, false);
            IFeature feature = featureCursor.NextFeature();
            while (feature != null)
            {
                OIDs.Add(feature.OID);
                feature = featureCursor.NextFeature();
            }
            Marshal.ReleaseComObject(featureCursor);
            Marshal.ReleaseComObject(spatialFilter);
            return OIDs;
        }

        private int Getid2(IFeature feature)
        {
            int id2 = Convert.ToInt32(feature.get_Value(feature.Fields.FindField("id2")));
            return id2;
        }
    }
}
