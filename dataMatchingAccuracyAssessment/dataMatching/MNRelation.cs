using ESRI.ArcGIS.Geodatabase;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using ESRI.ArcGIS.DataSourcesGDB;


namespace dataMatching
{
    public class MNRelation
    {

        /// <summary>
        /// 解析字段，获取OID
        /// </summary>
        /// <param name="textSOID"></param>
        /// <returns></returns>
        public static List<int> GetOIDs(string textOIDs)
        {
            List<int> OIDs = new List<int>();
            string[] arrOID = textOIDs.Split(',');
            for (int i = 0; i < arrOID.Length; i++)
            {
                if (arrOID[i] != "")
                {
                    int targetOID = -2;
                    if (int.TryParse(arrOID[i], out targetOID))
                    {
                        if (targetOID >= 0)
                        {
                            OIDs.Add(targetOID);
                        }
                    }
                }
            }
            return OIDs;
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
        /// 
        /// </summary>
        /// <param name="osmFeatCls"></param>
        public void Excute(IFeatureClass osmFeatCls)
        {
            IDataset dataset = (IDataset)osmFeatCls;
            IWorkspace workspace = dataset.Workspace as IWorkspace;
            ITable resultTable = OpenTable(workspace as IWorkspace2, "res");//匹配结果表
            int iSource = resultTable.FindField("GD");
            int iTarget = resultTable.FindField("OSM");
            int iStepCount = resultTable.FindField("StepCount");

            IQueryFilter qf = new QueryFilterClass();
            qf.WhereClause = "IsCheck = 0";
            ICursor cursor = resultTable.Search(qf, false);
            IRow row = cursor.NextRow();
            List<int> sRes = null;
            List<int> tRes = null;
            List<int> rowAligns = null;
            while (row != null)
            {
                rowAligns = new List<int>();
                rowAligns.Add(row.OID);
                sRes = new List<int>();
                tRes = new List<int>();
                List<int> sNewOIDs = new List<int>();
                List<int> sOIDs = GetOIDs(row.get_Value(iSource).ToString());
                for (int i = 0; i < sOIDs.Count; i++)
                {
                    sNewOIDs.Add(sOIDs[i]);
                    sRes.Add(sOIDs[i]);
                }
                List<int> tOIDs = GetOIDs(row.get_Value(iTarget).ToString());
                for (int i = 0; i < tOIDs.Count; i++)
                    tRes.Add(tOIDs[i]);

                IQueryFilter qf2 = new QueryFilterClass();
                ICursor cursor2 = null;
                IRow row2 = null;
                List<int> sOIDs2 = null;
                List<int> tOIDs2 = null;
                while (true)
                {
                    List<int> sNewOIDs2 = new List<int>();
                    for (int i = 0; i < sNewOIDs.Count; i++)
                    {
                        qf2.WhereClause = "IsCheck = 0 AND GD LIKE '%" + sNewOIDs[i] + "%'";
                        cursor2 = resultTable.Search(qf2, false);
                        row2 = cursor2.NextRow();
                        while (row2 != null)
                        {
                            if (!rowAligns.Contains(row2.OID))
                            {
                                rowAligns.Add(row2.OID);
                                sOIDs2 = GetOIDs(row2.get_Value(iSource).ToString());
                                if (sOIDs2.Contains(sNewOIDs[i]))
                                {
                                    for (int j = 0; j < sOIDs2.Count; j++)
                                    {
                                        if (!sRes.Contains(sOIDs2[j]))
                                        {
                                            sNewOIDs2.Add(sOIDs2[j]);
                                            sRes.Add(sOIDs2[j]);
                                        }
                                    }
                                    tOIDs2 = GetOIDs(row2.get_Value(iTarget).ToString());
                                    for (int j = 0; j < tOIDs2.Count; j++)
                                    {
                                        if (!tRes.Contains(tOIDs2[j]))
                                            tRes.Add(tOIDs2[j]);
                                    }
                                }
                            }
                            row2 = cursor2.NextRow();
                        }
                    }
                    if (sNewOIDs2.Count == 0)
                        break;
                    else
                    {
                        sNewOIDs.Clear();
                        for (int i = 0; i < sNewOIDs2.Count; i++)
                        {
                            sNewOIDs.Add(sNewOIDs2[i]);
                        }
                    }
                }
                //开始处理结果
                if (rowAligns.Count > 1)
                {
                    this.ModefiyTable(workspace, resultTable, rowAligns, sRes, tRes);
                }
                if (row2 != null) Marshal.ReleaseComObject(row2);
                if (cursor2 != null) Marshal.ReleaseComObject(cursor2);
                row = cursor.NextRow();
            }
        }

        private void ModefiyTable(IWorkspace workspace, ITable resultTable, List<int> rowAligns, List<int> sRes, List<int> tRes)
        {
            // 0:空匹配, 1:1对1匹配, 2:1对多匹配，3：多对1，5：M:N匹配
            if (rowAligns.Count > 1)
            {
                IWorkspaceEdit workspaceEdit = workspace as IWorkspaceEdit;
                int iSource = resultTable.FindField("GD");
                int iTarget = resultTable.FindField("OSM");
                int iIsCheck = resultTable.FindField("IsCheck"); 
                int iMatchType = resultTable.FindField("MatchType");
                workspaceEdit.StartEditing(true);
                workspaceEdit.StartEditOperation();
                IRow row = resultTable.GetRow(rowAligns[0]);
                row.set_Value(iSource, GetOIDsText(sRes));
                row.set_Value(iTarget, GetOIDsText(tRes));
                row.set_Value(iIsCheck, -100);
                if (sRes.Count>1 && tRes.Count==1)
                    row.set_Value(iMatchType, 3);
                if (sRes.Count > 1 && tRes.Count > 1)
                    row.set_Value(iMatchType, 5);
                row.Store();
                IRow row2 = null;
                for (int i=1;i< rowAligns.Count; i++)
                {
                    row2= resultTable.GetRow(rowAligns[i]);
                    row2.set_Value(iIsCheck, rowAligns[0]);
                    row2.Store();
                }
                workspaceEdit.StopEditOperation();
                workspaceEdit.StopEditing(true);
                if (row != null) Marshal.ReleaseComObject(row);
                if (row2 != null) Marshal.ReleaseComObject(row2);
            }

        }

    }
}
